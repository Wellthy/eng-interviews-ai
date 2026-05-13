import { MessageClassifier } from './components/MessageClassifier';

function App() {
  return (
    <div className="mx-auto max-w-3xl p-5 font-sans">
      <h1 className="mb-5 text-3xl font-bold">Urgent Message Flagger</h1>
      <MessageClassifier />
    </div>
  );
}

export default App;
