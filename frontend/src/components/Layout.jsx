   import { NavLink, Outlet, useLocation } from 'react-router-dom'

   const LINKS = [
     { to: '/deterministic', label: 'Deterministic', keepFilters: true },
     { to: '/ai', label: 'AI-adjusted', keepFilters: true },
     { to: '/comparison', label: 'Comparison', keepFilters: true },
     { to: '/upload', label: 'Upload', keepFilters: false },
   ]

   export function Layout() {
     const { search } = useLocation() // the "?currency=EUR..." part of the address

     return (
       <div className="min-h-screen bg-slate-100">
         <header className="border-b border-slate-200 bg-white">
           <div className="mx-auto flex max-w-6xl items-center gap-6 px-4 py-3">
             <span className="text-lg font-semibold text-slate-900">
               Liquid<span className="text-teal-700">+</span>
             </span>
             <nav className="flex gap-1">
               {LINKS.map((link) => (
                 <NavLink
                   key={link.to}
                   to={{ pathname: link.to, search: link.keepFilters ? search : '' }}
                   className={({ isActive }) =>
                     `rounded-md px-3 py-1.5 text-sm font-medium ${
                       isActive ? 'bg-teal-50 text-teal-800' : 'text-slate-600 hover:bg-slate-100'
                     }`
                   }
                 >
                   {link.label}
                 </NavLink>
               ))}
             </nav>
           </div>
         </header>
         <main className="mx-auto max-w-6xl px-4 py-6">
           <Outlet />
         </main>
       </div>
     )
   }