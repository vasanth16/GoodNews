import { ref, onMounted } from 'vue'

const installPrompt = ref(null)
const isInstallable = ref(false)
const isInstalled = ref(false)

let initialized = false

export function usePWA() {
  if (!initialized) {
    initialized = true

    // Check if already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      isInstalled.value = true
    }

    // Listen for install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault()
      installPrompt.value = e
      isInstallable.value = true
    })

    // Listen for successful install
    window.addEventListener('appinstalled', () => {
      isInstalled.value = true
      isInstallable.value = false
      installPrompt.value = null
    })
  }

  async function install() {
    if (!installPrompt.value) return false

    installPrompt.value.prompt()
    const { outcome } = await installPrompt.value.userChoice

    if (outcome === 'accepted') {
      isInstallable.value = false
      installPrompt.value = null
      return true
    }

    return false
  }

  return {
    isInstallable,
    isInstalled,
    install,
  }
}
