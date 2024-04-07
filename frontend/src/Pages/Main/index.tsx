import React, { useState, type FC, useEffect } from 'react';
import Header from '../../static/Header';
import Footer from '../../static/Footer';

import Input from './components/Input';
import CardsList from './components/CardsList';
import { type RoutesDataType } from '@models/backend';
import axios from 'axios';
import { parseDataTrack } from '../../parser';
import { type EventCardType } from '@models/frontend';

const Main: FC = () => {
	const [events, setEvents] = useState<EventCardType[]>([]);

	useEffect(() => {
		axios
			.get<RoutesDataType>('/api/events')
			.then(({ data }) => {
				setEvents(parseDataTrack(data.events));
			})
			.catch((e) => {
				console.log(e);
			});
	}, []);

	return (
		<>
			<Header />
			<main>
				<Input />
				<CardsList events={events} />
			</main>
			<Footer />
		</>
	);
};

export default Main;
