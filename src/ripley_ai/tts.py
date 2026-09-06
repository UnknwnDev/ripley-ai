import wave

from piper import PiperVoice, SynthesisConfig


class TTS:
    CONFIG: SynthesisConfig|None = None
    VOICE: PiperVoice|None = None

    @staticmethod
    def initialize(
        volume: float = 0.5,
        length_scale: float = 1.0,
        noise_scale: float = 1.0,
        noise_w_scale: float = 1.0,
        normalize_audio: bool = True,
    ):
        """Initializes tts module   """
        TTS.CONFIG = SynthesisConfig(
            volume=volume,  # half as loud
            length_scale=length_scale,  # twice as slow
            noise_scale=noise_scale,  # more audio variation
            noise_w_scale=noise_w_scale,  # more speaking variation
            normalize_audio=normalize_audio,  # use raw audio from voice
        )
        TTS.VOICE = PiperVoice.load("data/voices/en_US-hfc_female-medium.onnx")

    @staticmethod
    def speak(text: str):
        assert TTS.VOICE is not None
        with wave.open("output.wav", "wb") as wav_file:
            TTS.VOICE.synthesize_wav(text, wav_file, syn_config=TTS.CONFIG)
