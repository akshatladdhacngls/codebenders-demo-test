import json
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler
from typing import Any, Dict
 
# Import the DevOps agent module
from agent import create_devops_agent, get_initial_state
 
class HealthCheckHandler(RequestHandler):
    def get(self) -> None:
        """Simple health check endpoint"""
        self.write({"status": "ok", "message": "DevOps Agent API is running"})
 
class DevOpsAgentHandler(RequestHandler):
    async def post(self) -> None:
        """Main endpoint to invoke the DevOps agent"""
        try:
            # Initialize the agent graph and state
            graph = create_devops_agent()
            initial_state = get_initial_state()
            # Get any custom parameters from request body
            try:
                body = json.loads(self.request.body) if self.request.body else {}
                # Merge any provided parameters with initial state
                custom_state = {**initial_state, **body}
            except json.JSONDecodeError:
                custom_state = initial_state
            # Run the DevOps agent
            result = graph.invoke(custom_state)
            # Ensure the result is JSON serializable
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(result, default=str))
        except Exception as e:
            self.set_status(500)
            self.write({
                "error": str(e),
                "status": "failed"
            })
 
def make_app() -> tornado.web.Application:
    return tornado.web.Application([
        (r"/health", HealthCheckHandler),
        (r"/api/deploy", DevOpsAgentHandler),
    ])
 
if __name__ == "__main__":
    app = make_app()
    port = 8080
    app.listen(port)
    print(f"DevOps Agent API server started on port {port}")
    print(f"Health check: http://localhost:{port}/health")
    print(f"Deploy endpoint: http://localhost:{port}/api/deploy")
    tornado.ioloop.IOLoop.current().start()