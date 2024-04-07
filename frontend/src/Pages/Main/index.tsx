import React, { useState, type FC, useEffect } from 'react';
import Header from '../../static/Header';
import Footer from '../../static/Footer';
import Registration from '../../components/Registration';

import Input from './components/Input';
import CardsList from './components/CardsList';
import { type RoutesDataType } from '@models/backend';
import axios from 'axios';
import { parseDataTrack } from '../../parser';
import { type EventCardType } from '@models/frontend';

const Main: FC = () => {
	const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
	const [isRegistered, setIsRegistered] = useState<boolean>(false);
	const [events, setEvents] = useState<EventCardType[]>([]);

	useEffect(() => {
		axios
			.get<RoutesDataType>('/api/events/routes')
			.then(({ data }) => {
				setEvents(parseDataTrack(data.events));
			})
			.catch((e) => {
				console.log(e);
			});
	}, []);

	const handleModalOpen = (): void => {
		setIsModalOpen(true);
	};

	const handleModalClose = (): void => {
		setIsModalOpen(false);
	};

	const handleRegistrationClick = (): void => {
		setIsRegistered(true);
	};

	return (
		<>
			<Header />
			<main>
				<Input />
				<CardsList events={events} />
			</main>
			<Footer />
			<Registration
				isOpen={isModalOpen}
				onClose={handleModalClose}
				onClick={handleRegistrationClick}
			/>
		</>
	);
};

export default Main;
