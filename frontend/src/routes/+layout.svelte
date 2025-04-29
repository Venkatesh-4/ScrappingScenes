<script lang="ts">
    import { page } from '$app/stores';
</script>

<div class="app">
    <nav>
        <div class="nav-content">
            <a href="/" class="logo">Student Results</a>
            <div class="nav-links">
                <a 
                    href="/" 
                    class:active={$page.url.pathname === '/'}
                >
                    Dashboard
                </a>
                <a 
                    href="/fetch" 
                    class:active={$page.url.pathname === '/fetch'}
                >
                    Fetch Results
                </a>
            </div>
        </div>
    </nav>

    <main>
        <slot />
    </main>
</div>

<style>
    .app {
        min-height: 100vh;
        background-color: #f3f4f6;
    }

    nav {
        background-color: white;
        border-bottom: 1px solid #e5e7eb;
        padding: 1rem;
        position: sticky;
        top: 0;
        z-index: 10;
    }

    .nav-content {
        max-width: 1200px;
        margin: 0 auto;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .logo {
        font-size: 1.25rem;
        font-weight: 600;
        color: #4f46e5;
        text-decoration: none;
    }

    .nav-links {
        display: flex;
        gap: 2rem;
    }

    .nav-links a {
        color: #4b5563;
        text-decoration: none;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        transition: all 0.2s;
    }

    .nav-links a:hover {
        color: #4f46e5;
        background-color: #f3f4f6;
    }

    .nav-links a.active {
        color: #4f46e5;
        background-color: #ede9fe;
    }

    main {
        min-height: calc(100vh - 4rem);
    }
</style>
