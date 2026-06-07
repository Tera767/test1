import { useEffect, useState } from "react"
import { useSearchParams } from "react-router-dom"

function Dashboard() {
  const [user, setUser] = useState(null)
  const [searchParams] = useSearchParams()

  useEffect(() => {
    const token = searchParams.get("token")
    if (token) {
      localStorage.setItem("token", token)
      // decode JWT payload
      const payload = JSON.parse(atob(token.split(".")[1]))
      setUser(payload)
    }
  }, [])

  if (!user) return <p>Loading...</p>

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <img src={user.picture} style={{ borderRadius: "50%" }} />
      <h2>Hello, {user.name}!</h2>
      <p>{user.email}</p>
    </div>
  )
}

export default Dashboard