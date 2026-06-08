import { useState } from 'react'
import './App.css'

function App() {
  const today = new Date().toISOString().split('T')[0]

  const [happiness, setHappiness] = useState(5)
  const [energy, setEnergy] = useState(5)
  const [stressed, setStressed] = useState(false)
  const [friendsFamily, setFriendsFamily] = useState(false)
  const [notes, setNotes] = useState('')
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setSaved(false)
    setError(null)
    try {
      const res = await fetch('http://localhost:8000/mood', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          date: today,
          happiness,
          energy,
          stressed,
          friends_family_time: friendsFamily,
          notes,
        }),
      })
      if (!res.ok) throw new Error(`Server error ${res.status}`)
      setSaved(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>Northstar</h1>
      <p className="date">{today}</p>

      <form onSubmit={handleSubmit}>
        <div className="field">
          <div className="field-header">
            <label htmlFor="happiness">Happiness</label>
            <span className="value">{happiness}</span>
          </div>
          <input id="happiness" type="range" min="1" max="10" value={happiness}
            onChange={e => setHappiness(Number(e.target.value))} />
          <div className="ticks"><span>1</span><span>10</span></div>
        </div>

        <div className="field">
          <div className="field-header">
            <label htmlFor="energy">Energy</label>
            <span className="value">{energy}</span>
          </div>
          <input id="energy" type="range" min="1" max="10" value={energy}
            onChange={e => setEnergy(Number(e.target.value))} />
          <div className="ticks"><span>1</span><span>10</span></div>
        </div>

        <div className="toggle-row" onClick={() => setStressed(s => !s)}>
          <span>Stressed?</span>
          <div className={`toggle ${stressed ? 'on' : ''}`}><div className="knob" /></div>
        </div>

        <div className="toggle-row" onClick={() => setFriendsFamily(f => !f)}>
          <span>Spent time with friends or family?</span>
          <div className={`toggle ${friendsFamily ? 'on' : ''}`}><div className="knob" /></div>
        </div>

        <div className="field">
          <label htmlFor="notes">Notes</label>
          <textarea id="notes" rows={3}
            placeholder="Anything worth noting? Sleep, alcohol, etc."
            value={notes} onChange={e => setNotes(e.target.value)} />
        </div>

        {saved && <p className="saved">Saved.</p>}
        {error && <p className="error">{error}</p>}

        <button type="submit" disabled={loading}>
          {loading ? 'Saving…' : 'Save today'}
        </button>
      </form>
    </div>
  )
}

export default App
