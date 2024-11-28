from pydantic import BaseModel
from typing import Optional

class TickerInfo(BaseModel):
    ticker: str = "Unknown"
    price: float = 0.0
    dy: float = 0.0
    pvp: float = 0.0
    segment: Optional[str] = None
    type_anbima: Optional[str] = None
    segment_anbima: Optional[str] = None
    roe: Optional[float] = None
    dl_ebitda: Optional[float] = None
    sector: Optional[str] = None
    sub_sector: Optional[str] = None

    def __str__(self) -> str:
        return f"""
            Ticker: {self.ticker}
            Price: {self.price}
            DY: {self.dy}
            PVP: {self.pvp}
            Segment: {self.segment}
            Type ANBIMA: {self.type_anbima}
            Segment ANBIMA: {self.segment_anbima}
            ROE: {self.roe}
            DL EBITDA: {self.dl_ebitda}
            Sector: {self.sector}
            Sub Sector: {self.sub_sector}
        """
    
    def __json__(self) -> dict:
        return self.dict()

    @staticmethod
    def convert_to_float(value: str) -> Optional[float]:
        if value.strip() == "-":
            return None
        return float(value.replace(".", "").replace(",", ".").replace("%", ""))

    def set_ticker(self, ticker: str) -> None:
        self.ticker = ticker

    def set_price(self, price: str) -> None:
        self.price = self.convert_to_float(price)

    def set_dy(self, dy: str) -> None:
        self.dy = self.convert_to_float(dy)

    def set_pvp(self, pvp: str) -> None:
        self.pvp = self.convert_to_float(pvp)

    def set_segment(self, segment: str) -> None:
        self.segment = segment

    def set_type_anbima(self, type_anbima: str) -> None:
        self.type_anbima = type_anbima

    def set_segment_anbima(self, segment_anbima: str) -> None:
        self.segment_anbima = segment_anbima

    def set_roe(self, roe: str) -> None:
        self.roe = self.convert_to_float(roe)

    def set_dl_ebitda(self, dl_ebitda: str) -> None:
        self.dl_ebitda = self.convert_to_float(dl_ebitda)

    def set_sector(self, sector: str) -> None:
        self.sector = sector

    def set_sub_sector(self, sub_sector: str) -> None:
        self.sub_sector = sub_sector