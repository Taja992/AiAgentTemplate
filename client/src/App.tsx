import './App.css'
import { ApiTest } from './components/system/ApiConnectionTest'
import { ChatPage } from './pages/Chat'

function App() {

  return (
    <>

      <div className="api-test">
        <ApiTest />
        <ChatPage />
      </div>

    </>
  )
}

export default App
