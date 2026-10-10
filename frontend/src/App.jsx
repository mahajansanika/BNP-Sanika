   import { Navigate, Route, Routes } from 'react-router-dom'
   import { Layout } from './components/Layout'
   import { AiLadderPage } from './pages/AiLadderPage'
   import { ComparisonPage } from './pages/ComparisonPage'
   import { DeterministicPage } from './pages/DeterministicPage'
   import { LoginPage } from './pages/loginPage'

   function Placeholder({ title }) {
     return <h1 className="text-xl font-semibold">{title}</h1>
   }

   export default function App() {
     return (
       <Routes>
         <Route path="/login" element={<LoginPage />} />
         <Route element={<Layout />}>
           <Route path="/" element={<Navigate to="/deterministic" replace />} />
           <Route path="/deterministic" element={<DeterministicPage />} />
           <Route path="/ai" element={<AiLadderPage />} />
           <Route path="/comparison" element={<ComparisonPage />} />
           <Route path="/upload" element={<Placeholder title="Upload (Dev 2)" />} />
           <Route path="*" element={<Placeholder title="Page not found" />} />
         </Route>
       </Routes>
     )
   }