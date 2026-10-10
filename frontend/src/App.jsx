   import { Link, Navigate, Route, Routes } from 'react-router-dom'
   import { AiLadderPage } from './pages/AiLadderPage'
   import { ComparisonPage } from './pages/ComparisonPage'
   import { DeterministicPage } from './pages/DeterministicPage'
   import { LoginPage } from './pages/loginPage'

   export default function App() {
     return (
       <div className="min-h-screen bg-slate-100 p-8">
         <nav className="mb-6 flex gap-4 text-sm text-teal-700">
           <Link to="/deterministic">Deterministic</Link>
           <Link to="/ai">AI</Link>
           <Link to="/comparison">Comparison</Link>
           <Link to="/login">Login</Link>
         </nav>
         <Routes>
           <Route path="/" element={<Navigate to="/deterministic" replace />} />
           <Route path="/login" element={<LoginPage />} />
           <Route path="/deterministic" element={<DeterministicPage />} />
           <Route path="/ai" element={<AiLadderPage />} />
           <Route path="/comparison" element={<ComparisonPage />} />
         </Routes>
       </div>
     )
   }