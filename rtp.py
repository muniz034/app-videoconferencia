from rtp import RTPPacket

class RTPInterface:
    def parse(data):
        return RTPPacket.parse(data)

    def pack(PAYLOAD_TYPE, data):
        return RTPPacket(payload_type=PAYLOAD_TYPE, data=data).pack()
