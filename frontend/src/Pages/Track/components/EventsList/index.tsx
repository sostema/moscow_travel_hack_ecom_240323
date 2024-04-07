import React, { type FC } from 'react';
import { type EventCardType } from '../../../../models/frontend';
import Walk from './Walk';
import Event from './Event';

import styles from './EventsList.module.scss';

interface EventsListProps {
	events: EventCardType[];
	onClick: (event: EventCardType) => void;
}

const EventsList: FC<EventsListProps> = ({ events, onClick }) => {
	let queue = 0;

	return (
		<div className={styles.root}>
			{events.map((event, index) => {
				if (event.type === 'EVENT' || event.type === 'RESTAURANT') {
					queue++;
					return <Event key={event.id} onClick={onClick} queue={queue} event={event} />;
				}

				if (event.type === 'WALK') {
					return <Walk key={event.id} {...event} />;
				}

				return null;
			})}
		</div>
	);
};

export default EventsList;
