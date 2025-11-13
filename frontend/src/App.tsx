import styles from "./App.module.css"

function App() {

  return (
      <div className={styles.mainContent}>
        <div className={styles.banner}>
          <button>Home</button>
          <h2>Connect 4</h2>
          <button>Login</button>
        </div>
        <canvas></canvas>
      </div>
  )
}

export default App
