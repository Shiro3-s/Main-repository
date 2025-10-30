import Saludo from "./saludo"
import Apellido from "./apellido"

const concatenar = ({Saludo, Apellido}) => {
    return <><h1>Hola {Saludo + " " + Apellido}</h1></>
}

export default concatenar