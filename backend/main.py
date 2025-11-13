import uvicorn
from app import run

app = run()

def main() -> None:
    uvicorn.run("main:app", reload=True)

if __name__ == "__main__":
    main()