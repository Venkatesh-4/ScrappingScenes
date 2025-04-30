<script lang="ts">
  let output: string = "";
  let error: string = "";
  let success: boolean = false;
  let loading: boolean = false;
  let username: string = "";
  let password: string = "";

  async function runFetcher() {
    loading = true;
    output = "";
    error = "";
    success = false;

    try {
      const response = await fetch('http://localhost:8000/api/run-fetcher', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
      });

      const data = await response.json();

      if (data.success) {
        output = data.output;
        error = data.error;
        success = true;
      } else {
        error = data.error || 'Failed to run fetcher';
        success = false;
      }
    } catch (e) {
      error = e.message;
      success = false;
    } finally {
      loading = false;
    }
  }
</script>

<div class="container">
  <h1>Fetch Results</h1>

  <div class="login-card">
    <form on:submit|preventDefault={runFetcher}>
      <div class="form-group">
        <label for="username">Username</label>
        <input
          type="email"
          id="username"
          bind:value={username}
          placeholder="Enter your email"
          required
        />
      </div>

      <div class="form-group">
        <label for="password">Password</label>
        <input
          type="password"
          id="password"
          bind:value={password}
          placeholder="Enter your password"
          required
        />
      </div>

      <button type="submit" disabled={loading} class="submit-button">
        {loading ? 'Running...' : 'Run Fetcher'}
      </button>
    </form>
  </div>

  {#if success}
    <div class="success-box">
      <div class="success-icon">✅</div>
      <div class="success-message">Operation completed successfully!</div>
    </div>
  {/if}

  {#if error}
    <div class="error-box">
      <div class="error-icon">⚠️</div>
      <div class="error-message">{error}</div>
    </div>
  {/if}

  {#if output}
    <div class="terminal">
      <pre>{output}</pre>
    </div>
  {/if}
</div>

<style>
  .container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }

  h1 {
    font-size: 2rem;
    font-weight: bold;
    margin-bottom: 2rem;
    color: #333;
    text-align: center;
  }

  .login-card {
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
  }

  .form-group {
    margin-bottom: 1rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 500;
    color: #333;
  }

  input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
    margin-bottom: 1rem;
  }

  input:focus {
    outline: none;
    border-color: #4a90e2;
    box-shadow: 0 0 0 2px rgba(74, 144, 226, 0.2);
  }

  .submit-button {
    width: 100%;
    padding: 0.75rem;
    background-color: #4a90e2;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
  }

  .submit-button:hover:not(:disabled) {
    background-color: #357abd;
  }

  .submit-button:disabled {
    opacity: 0.7;
    cursor: not-allowed;
  }

  .success-box {
    background-color: #e8f5e9;
    border-left: 4px solid #4caf50;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 4px;
    display: flex;
    align-items: flex-start;
  }

  .success-icon {
    margin-right: 0.5rem;
  }

  .success-message {
    color: #2e7d32;
    font-size: 0.9rem;
  }

  .error-box {
    background-color: #ffebee;
    border-left: 4px solid #ef5350;
    padding: 1rem;
    margin-bottom: 1rem;
    border-radius: 4px;
    display: flex;
    align-items: flex-start;
  }

  .error-icon {
    margin-right: 0.5rem;
  }

  .error-message {
    color: #c62828;
    font-size: 0.9rem;
  }

  .terminal {
    background-color: #1e1e1e;
    border-radius: 8px;
    padding: 1rem;
    margin-top: 1rem;
    overflow-x: auto;
  }

  .terminal pre {
    margin: 0;
    color: #00ff00;
    font-family: 'Courier New', monospace;
    white-space: pre-wrap;
    word-break: break-word;
  }

  :global(body) {
    background-color: #f5f5f5;
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  }
</style>
