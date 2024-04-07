import React, { useState, type FC, useEffect } from 'react';
import Header from '../../static/Header';
import Footer from '../../static/Footer';

import Input from './components/Input';
import CardsList from './components/CardsList';
import { type RoutesDataType } from '@models/backend';
import axios from 'axios';
import { parseDataTrack } from '../../parser';
import { type EventCardType } from '@models/frontend';

import RussPass from '@media/rus_pass.svg?react';
import { useNavigate } from 'react-router-dom';

import { ToastContainer, toast } from 'react-toastify';

import 'react-notifications/lib/notifications.css';
import Registration from '@components/Registration';

const Main: FC = () => {
	const [events, setEvents] = useState<EventCardType[]>([]);
	const [isRegistered, setIsRegistered] = useState(false);
	const [openModal, setOpenModal] = useState(false);
	const navigate = useNavigate();

	// eslint-disable-next-line @typescript-eslint/explicit-function-return-type
	const notify = () => toast(<>У нас есть для вас сюрпиз!</>);
	// title: 'У нас есть для вас сюрпиз!',
	// message: 'Посмотрите что мы для вас подобрали.',

	useEffect(() => {
		if (isRegistered) {
			setTimeout(notify, 3000);
		}
	}, [isRegistered]);

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

	const handleButtonClick = (): void => {
		if (!isRegistered) {
			handleModalOpen();
		} else {
			window.open('/track', '_blank');
		}
	};

	const handleModalOpen = (): void => {
		setOpenModal(true);
	};

	const handleModalClose = (): void => {
		setOpenModal(false);
	};

	const handleRegistrationClick = (): void => {
		setIsRegistered(true);
		setOpenModal(false);
	};

	return (
		<>
			<Header authClick={handleButtonClick} />
			<main>
				<Input />
				<CardsList events={events} />
			</main>
			<Footer />
			<ToastContainer
				onClick={() => {
					navigate('/track');
				}}
				icon={RussPass}
				position="top-left"
			/>
			<Registration
				isOpen={openModal}
				onClose={handleModalClose}
				onClick={handleRegistrationClick}
			/>
		</>
	);
};

export default Main;
