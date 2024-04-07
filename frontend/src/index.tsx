import React from 'react';
import ReactDOM from 'react-dom/client';

import './index.scss';
import Track from './Pages/Track';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import Main from './Pages/Main';

const router = createBrowserRouter([
	{
		path: '/',
		element: <Main />,
	},
	{
		path: '/track/',
		element: <Track />,
	},
]);

// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
ReactDOM.createRoot(document.getElementById('root')!).render(
	<React.StrictMode>
		<RouterProvider router={router} />
	</React.StrictMode>,
);
