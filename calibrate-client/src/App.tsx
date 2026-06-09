import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Introduction from './pages/intro/introduction';
import Monitor from './pages/monitor/monitor';
import Setup from './pages/setup/setup';
import SetupContextProvider from './contexts/setup-context';
import HeaderContextProvider from './contexts/header-context';


function App() {
  return (
    <SetupContextProvider>
		<HeaderContextProvider>
			<BrowserRouter>
				<Routes>
					<Route path="/" element={<Introduction />}/>
					<Route path="/setup" element={<Setup />} />
					<Route path="/monitor" element={<Monitor />} />
				</Routes>
			</BrowserRouter>
		</HeaderContextProvider>
	</SetupContextProvider>
  )
}

export default App
