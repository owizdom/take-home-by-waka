"""
SQLAlchemy model + helpers for the algo_analysis table.
"""
from sqlalchemy import create_engine, Column, Integer, Float, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

# ── Connection ────────────────────────────────────────────────────────
DB_URL = "sqlite:///algo_analyzer.db"
engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# ── Model ─────────────────────────────────────────────────────────────
class AlgoAnalysis(Base):
    """Stores the result of a single algorithm analysis run."""
    __tablename__ = "algo_analysis"

    id              = Column(Integer, primary_key=True, autoincrement=True)
    algo            = Column(String(64),  nullable=False)
    items           = Column(Integer,     nullable=False)
    steps           = Column(Integer,     nullable=False)
    start_time      = Column(Float,       nullable=False)
    end_time        = Column(Float,       nullable=False)
    total_time_ms   = Column(Float,       nullable=False)
    time_complexity = Column(String(32),  nullable=False)
    graph_base64    = Column(Text,        nullable=False)   # base-64 PNG

    def to_dict(self):
        return {
            "id":              self.id,
            "algo":            self.algo,
            "items":           self.items,
            "steps":           self.steps,
            "start_time":      self.start_time,
            "end_time":        self.end_time,
            "total_time_ms":   self.total_time_ms,
            "time_complexity": self.time_complexity,
            "graph_base64":    self.graph_base64,
        }


def init_db():
    """Create all tables that don't exist yet."""
    Base.metadata.create_all(engine)
