from rgn.serve import cli

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "serve":
        import uvicorn

        uvicorn.run("rgn.main:app", host="127.0.0.1", port=4444, reload=True)
    else:
        cli()
