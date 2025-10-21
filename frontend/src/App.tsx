import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Home from './pages/Home'
import Upload from './pages/Upload'
import Config from './pages/Config'
import MimicMe from './pages/MimicMe'
import KnowMyself from './pages/KnowMyself'
import RememberMe from './pages/RememberMe'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/config" element={<Config />} />
          <Route path="/mimic" element={<MimicMe />} />
          <Route path="/analysis" element={<KnowMyself />} />
          <Route path="/memory" element={<RememberMe />} />
        </Routes>
      </Layout>
    </Router>
  )
}

export default App
