import React, { type FC, useEffect, useState, useCallback } from 'react';

import HumanIcon from '../../media/human_walk.svg?react';

import Button from './components/Button';
import Title from './components/Title';

import styles from './styles.module.scss';
import axios from 'axios';
import { type RoutesDataType } from '../../models/backend';
import { intervalToDuration } from 'date-fns';
import { parseDataTrack } from '../../parser';
import { type EventCardType } from '../../models/frontend';
import EventsList from './components/EventsList';
import Card from '../../components/Card';
import Header from '../../static/Header';
import Footer from '../../static/Footer';
import Registration from '@components/Registration';

const Track: FC = () => {
	const [time, setTime] = useState<string>('');
	const [distance, setDistance] = useState<string>('');
	const [events, setEvents] = useState<EventCardType[]>([]);
	const [activeEvent, setActiveEvent] = useState<EventCardType | undefined>(undefined);
	const [name, setName] = useState<string>('');
	const [isRegistered, setIsRegistered] = useState(false);
	const [showModal, setShowModal] = useState(false);

	const handleEventClick = (event: EventCardType): void => {
		setActiveEvent(event);
	};

	useEffect(() => {
		axios
			.get<RoutesDataType>('/api/events/routes')
			.then(({ data }) => {
				const duration = intervalToDuration({ start: 0, end: data.time * 1000 });
				let formattedTime = '';
				if (duration.hours) {
					formattedTime = formattedTime + `${duration.hours}ч`;
				}

				if (duration.minutes) {
					formattedTime = formattedTime + `${duration.minutes}мин`;
				}
				const formattedDistance = data.distance;

				setTime(formattedTime);
				setDistance(`${formattedDistance}км`);
				setEvents(parseDataTrack(data.events));
				setActiveEvent(parseDataTrack(data.events)[0]);
			})
			.catch((e) => {
				console.log(e);
			});
	}, []);

	const handleButtonClick = useCallback(() => {
		if (!isRegistered) {
			setShowModal(true);
		} else if (activeEvent) {
			window.open(activeEvent.link, '_blank');
		}
	}, [activeEvent, isRegistered]);

	const handleClickRegister = (): void => {
		setIsRegistered(true);
		setShowModal(false);
	};

	useEffect(() => {
		if (activeEvent) {
			setName(activeEvent?.name);
		}
	}, [activeEvent]);

	return (
		<>
			<Header />
			<main className="layoutNota_background__IzYDA layoutNota_content__MlFYT">
				<div className="planDetails_container__Kdl9G">
					<div className="planDetails_contentWrap__xh8J_">
						<div className="planHeader_contentWrapper__vrbiy">
							<div className="planHeader_content__QHQTX">
								<div className={styles.title}>
									<Title text={name} />
								</div>
								<div className="" data-tour="onboarding-plan-header">
									<Button onClick={handleButtonClick} />
								</div>
							</div>
						</div>
					</div>
					<div className={styles.wrapper}>
						<div className={styles.timedistance}>
							<HumanIcon />
							<span className={styles.time}>{time}</span>
							<span className={styles.distance}>{distance}</span>
						</div>
					</div>
					<div className={styles.container}>
						<EventsList onClick={handleEventClick} events={events} />
						{activeEvent && <Card onClick={handleButtonClick} {...activeEvent} />}
					</div>
				</div>
			</main>
			<Footer />
			<Registration
				onClick={handleClickRegister}
				isOpen={showModal}
				onClose={() => {
					setShowModal(false);
				}}
			/>
		</>
	);
};

export default Track;
