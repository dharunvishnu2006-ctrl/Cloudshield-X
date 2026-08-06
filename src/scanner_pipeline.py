class PipelineStage:
    """One stage in the scanner pipeline - a name, a function to run, and a link
    to the next stage."""

    def __init__(self, name: str, action):
        self.name = name
        self.action = action
        self.next = None

    def run(self, data):
        """Run this stage's action, then pass the result to the next stage."""
        print(f"-> running stage: {self.name}")
        result = self.action(data)
        if self.next is not None:
            return self.next.run(result)
        return result
