export default function Home() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">AI Test Scenario Generator</h1>
      <p>Enter Jira Ticket ID below</p>

      <input className="border p-2 mt-4" placeholder="JIRA-123" />

      <button className="bg-blue-500 text-white p-2 ml-2">
        Fetch
      </button>
    </div>
  );
}