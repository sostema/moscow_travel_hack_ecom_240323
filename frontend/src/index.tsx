import React from 'react';
import ReactDOM from 'react-dom/client';

import Header from './static/Header';

import './index.scss';
import Footer from './static/Footer';
import App from './Pages/Track';

// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
ReactDOM.createRoot(document.getElementById('root')!).render(
	<React.StrictMode>
		<Header />
		<App />
		<Footer />
	</React.StrictMode>,
);
