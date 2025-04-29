import sqlite3
import uuid
from dataclasses import dataclass
from typing import Literal
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
import asyncio

conn = sqlite3.connect(":memory:")
conn.execute("""
    CREATE TABLE tickets (
        ticket_id TEXT PRIMARY KEY,
        summary   TEXT NOT NULL,
        severity  TEXT NOT NULL,
        department TEXT NOT NULL,
        status    TEXT NOT NULL
    )
""")
conn.commit()

@dataclass
class TicketingDependencies:
    """Carries our DB connection into system prompts and tools."""
    db: sqlite3.Connection


class CreateTicketOutput(BaseModel):
    ticket_id: str = Field(..., description="Unique ticket identifier")
    summary: str   = Field(..., description="Text summary of the issue")
    severity: Literal["low","medium","high"] = Field(..., description="Urgency level")
    department: str = Field(..., description="Responsible department")
    status: Literal["open"] = Field("open", description="Initial ticket status")


class TicketStatusOutput(BaseModel):
    ticket_id: str = Field(..., description="Unique ticket identifier")
    status: Literal["open","in_progress","resolved"] = Field(..., description="Current ticket status")

create_agent = Agent(
    'groq:meta-llama/llama-4-scout-17b-16e-instruct',
    deps_type=TicketingDependencies,
    output_type=CreateTicketOutput,
    system_prompt="Você é um assistente de análise de tickets. Use a tool 'create_ticket' para o log de novos problemas."
)

@create_agent.tool
async def create_ticket(
    ctx: RunContext[TicketingDependencies],
    summary: str,
    severity: Literal["low","medium","high"],
    department: str
) -> CreateTicketOutput:
    """
    Logs a new ticket in the database.
    """
    tid = str(uuid.uuid4())
    ctx.deps.db.execute(
        "INSERT INTO tickets VALUES (?,?,?,?,?)",
        (tid, summary, severity, department, "open")
    )
    ctx.deps.db.commit()
    return CreateTicketOutput(
        ticket_id=tid,
        summary=summary,
        severity=severity,
        department=department,
        status="open"
    )

status_agent = Agent(
    'groq:meta-llama/llama-4-scout-17b-16e-instruct',
    deps_type=TicketingDependencies,
    output_type=TicketStatusOutput,
    system_prompt = """
            Você é um assistente de análise de tickets.
            Use sempre a ferramenta 'create_ticket' para registrar novos problemas.
            Certifique-se de preencher exatamente estes campos:
            - summary: resumo do problema
            - severity: um dos seguintes ["low", "medium", "high"]
            - department: departamento responsável, por exemplo "TI", "RH", "Manutenção"
            """

)

@status_agent.tool
async def get_ticket_status(
    ctx: RunContext[TicketingDependencies],
    ticket_id: str
) -> TicketStatusOutput:
    """
    Fetches the ticket status from the database.
    """
    cur = ctx.deps.db.execute(
        "SELECT status FROM tickets WHERE ticket_id = ?", (ticket_id,)
    )
    row = cur.fetchone()
    if not row:
        raise ValueError(f"No ticket found for ID {ticket_id!r}")
    return TicketStatusOutput(ticket_id=ticket_id, status=row[0])

deps = TicketingDependencies(db=conn)

async def main():
    deps = TicketingDependencies(db=conn)

    create_result = await create_agent.run(
    "Estou com problemas com meu computador. Ele liga, mas só mostra uma tela azul.", deps=deps
    )

    print("Created Ticket →")
    print(create_result.output.model_dump_json(indent=2))

    tid = create_result.output.ticket_id
    status_result = await status_agent.run(
        f"What's the status of ticket {tid}?", deps=deps
    )

    print("Ticket Status →")
    print(status_result.output.model_dump_json(indent=2))

# Executa o main
asyncio.run(main())