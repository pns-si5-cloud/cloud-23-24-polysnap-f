import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useParams,
  useNavigate
} from "react-router-dom";
import MessageInput from "./components/MessageInput";
import MessageList from "./components/MessageList";
import ConversationsList from "./components/ConversationsList";
import Stories from "./components/stories";
import "./App.css";

function UserPage() {
  const { userID } = useParams();
  const [selectedConversation, setSelectedConversation] = useState(null);

  return (
    <div style={{ display: "flex" }}>
      <div style={{ flex: "30%", borderRight: "1px solid gray" }}>
        <Stories userID={userID} />

        <ConversationsList
          userID={userID}
          setSelectedConversation={setSelectedConversation}
          selectedConversation={selectedConversation}
        />
      </div>
      <div style={{ flex: "70%" }}>
        {selectedConversation ? (
          <>
            <MessageList
              userID={userID}
              conversationId={selectedConversation}
            />
            <MessageInput
              userID={userID}
              conversationId={selectedConversation}
            />
          </>
        ) : (
          <p>Please select a conversation or start a new one.</p>
        )}
      </div>
    </div>
  );
}

function EnterUserID() {
  const [inputUserID, setInputUserID] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();
    navigate(`/${inputUserID}`); // Redirige vers la route avec le userID
  };

  return (
    <div className="enterUserIdForm">
      <form onSubmit={handleSubmit}>
        <label htmlFor="userID">Enter User ID:</label>
        <input
          type="text"
          id="userID"
          value={inputUserID}
          onChange={(e) => setInputUserID(e.target.value)}
        />
        <button type="submit">Go</button>
      </form>
    </div>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<EnterUserID />} />
          <Route path="/:userID" element={<UserPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

