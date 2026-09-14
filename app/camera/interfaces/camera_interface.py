from abc import ABC, abstractmethod


class CameraInterface(ABC):
    """Any camera backend (laptop webcam, Pi camera, mock/test) implements this."""

    @abstractmethod
    def start(self):
        ...

    @abstractmethod
    def read(self):
        """Returns (success: bool, frame: np.ndarray | None) in BGR format."""
        ...

    @abstractmethod
    def stop(self):
        ...