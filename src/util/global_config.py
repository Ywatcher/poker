# -*- coding: utf-8 -*-
force_cpu = "cpu"
auto = "auto"

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

    def override(self, attrs):
        if isinstance(attrs, dict):
            self.__dict__.update(**attrs)
        elif isinstance(attrs, (list, tuple, set)):
            for attr in attrs:
                self.override(attr)
        elif attrs is not None:
            raise NotImplementedError
        return self
# audio_params = AttrDict(
#     sample_rate=16000,  # todo
#     n_mels=80,
#     n_fft=1024,
#     hop_samples=256,
#     crop_mel_frames=62,
#     # clip_span=3
#     clip_span=1
# )

window_size = AttrDict(
    w=1024,
    h=768
)


class GlobalConfigTable:

    def __init__(self):
        self.__device = "cpu"
        self.w=1024
        self.h=768

    def setDevice(self, device=auto):
        """
        :param device: "CPU" or "GPU" or "auto"
        :return: null
        """
        assert device == force_cpu or device == auto
        self.__device = device

    def device(self) -> str:
        return self.__device
