package com.example.cameras2usb

import java.nio.ByteBuffer

object H264toMPEGTS {

    private const val TS_PACKET_SIZE = 188
    private const val SYNC_BYTE: Byte = 0x47

    private var continuityCounter = 0

    // IDs de stream
    private const val PAT_PID = 0x0000
    private const val PMT_PID = 0x100
    private const val VIDEO_PID = 0x101

    // Paquete PAT fijo
    private fun createPAT(): ByteArray {
        val pat = ByteArray(TS_PACKET_SIZE)
        pat[0] = SYNC_BYTE
        pat[1] = 0x40
        pat[2] = 0x00
        pat[3] = 0x10
        // Payload: tabla PAT mínima
        pat[4] = 0x00  // table_id
        pat[5] = 0xB0.toByte()  // section_syntax_indicator + length
        pat[6] = 0x0D  // section length
        pat[7] = 0x00  // transport_stream_id
        pat[8] = 0x01
        pat[9] = 0xC1.toByte()  // version_number + current_next_indicator
        pat[10] = 0x00 // section_number
        pat[11] = 0x00 // last_section_number
        pat[12] = 0x00 // program_number
        pat[13] = 0x01
        pat[14] = 0xE0.toByte() // program_map_PID
        pat[15] = 0x10
        // CRC simple (no es crítico)
        pat[16] = 0x2A
        pat[17] = 0xB1.toByte()
        pat[18] = 0x04
        pat[19] = 0xB2.toByte()
        return pat
    }

    // Paquete PMT fijo
    private fun createPMT(): ByteArray {
        val pmt = ByteArray(TS_PACKET_SIZE)
        pmt[0] = SYNC_BYTE
        pmt[1] = (0x40 or ((PMT_PID shr 8) and 0x1F).toByte().toInt()).toByte()
        pmt[2] = (PMT_PID and 0xFF).toByte()
        pmt[3] = 0x10
        pmt[4] = 0x02 // table_id
        pmt[5] = 0xB0.toByte() // section_syntax_indicator + length
        pmt[6] = 0x0D
        pmt[7] = 0x00
        pmt[8] = 0x01 // program_number
        pmt[9] = 0xC1.toByte() // version + current_next
        pmt[10] = 0x00 // section_number
        pmt[11] = 0x00 // last_section_number
        pmt[12] = 0xE1.toByte() // PCR_PID
        pmt[13] = 0x01
        pmt[14] = 0xF0.toByte() // program info length
        pmt[15] = 0x00
        // Stream descriptor: video H.264
        pmt[16] = 0x1B // stream_type (H.264)
        pmt[17] = 0xE1.toByte()
        pmt[18] = 0x01 // elementary PID
        pmt[19] = 0xF0.toByte() // ES info length
        pmt[20] = 0x00
        // CRC simple
        pmt[21] = 0x2A
        pmt[22] = 0xB1.toByte()
        pmt[23] = 0x04
        pmt[24] = 0xB2.toByte()
        return pmt
    }

    fun createTSStream(h264Data: ByteArray): ByteArray {
        val tsStream = mutableListOf<Byte>()

        // Insertamos PAT y PMT al inicio
        tsStream.addAll(createPAT().toList())
        tsStream.addAll(createPMT().toList())

        // Fragmentamos el frame H.264 en paquetes TS
        var offset = 0
        while (offset < h264Data.size) {
            val packet = ByteArray(TS_PACKET_SIZE)
            packet[0] = SYNC_BYTE
            packet[1] = (0x40 or ((VIDEO_PID shr 8) and 0x1F).toByte().toInt()).toByte()
            packet[2] = (VIDEO_PID and 0xFF).toByte()
            packet[3] = (0x10 or (continuityCounter and 0x0F)).toByte()

            continuityCounter = (continuityCounter + 1) % 16

            val copySize = minOf(TS_PACKET_SIZE - 4, h264Data.size - offset)
            System.arraycopy(h264Data, offset, packet, 4, copySize)
            offset += copySize

            tsStream.addAll(packet.toList())
        }

        return tsStream.toByteArray()
    }
}
