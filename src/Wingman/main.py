import threading
from Wingman.core.input_receiver import InputReceiver
from Wingman.core.session import GameSession
from Wingman.core.network_listener import NetworkListener
from Wingman.gui.app import XPTrackerApp

if __name__ == "__main__":
    # Create the SHARED receiver
    shared_receiver = InputReceiver()

    # Pass it to both
    listener = NetworkListener(shared_receiver)
    session = GameSession(shared_receiver)

    # Start app
    app = XPTrackerApp(session)
    listener.start()
    app.run()