function Login() {
  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>Welcome</h1>
      <a href="http://localhost:8000/auth/login">
        <button>Sign in with Google</button>
      </a>
    </div>
  )
}

export default Login