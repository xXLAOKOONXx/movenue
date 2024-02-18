from abc import abstractmethod, ABC


class BaseCard(ABC):
  @abstractmethod
  def get_poster(self, master):
    pass
  @abstractmethod
  def calculate_score(self) -> int:
    pass