import {BrowserRouter, Routes, Route} from "react-router-dom"
import{CrearCliente} from "./page//crearcliente"
import {ListaCliente} from "./page//listacliente"
import {Navegacion} from "./components//navegacion"
import {Toaster} from 'react-hot-toast'

function App() {
  return (
    <BrowserRouter>
     <div className="container mx-auto">
      <Navegacion/>
      <Routes>
       <Route path="/crear-cliente" element={<CrearCliente/>} /> 
       <Route path="/lista-clientes" element={<ListaCliente/>} /> 
       <Route path="/clientes/:id" element={<CrearCliente/>} /> 
      </Routes>
      <Toaster/>
    </div>
    </BrowserRouter>
  )
}

export default App
