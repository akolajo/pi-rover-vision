from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Detection:
    """A single detected object, in pixel coordinates of the source frame."""
    label: str
    confidence: float
    x: int
    y: int
    w: int
    h: int

    @property
    def center(self):
        return (self.x + self.w // 2, self.y + self.h // 2)


class DetectorInterface(ABC):
    """Any detection strategy (colour blob, TFLite, future ones) implements
    this. Detectors only read frames and return detections. They never draw
    on the frame and never touch the camera or GPIO, so they stay testable
    off the Pi."""

    @abstractmethod
    def detect(self, frame) -> list[Detection]:
        ...