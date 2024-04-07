import React, { useCallback, type FC } from 'react';
import { type EventCardType } from '../../../../../models/frontend';

import styles from './Event.module.scss';

interface EventProps {
	event: EventCardType;
	queue: number;
	onClick: (event: EventCardType) => void;
}

const Event: FC<EventProps> = ({ onClick, queue, event }) => {
	const { imgLink, time, name, address } = event;

	const handleOnClick = useCallback(() => {
		onClick(event);
	}, [event]);

	return (
		<button className={styles.root} onClick={handleOnClick}>
			<div className={styles.image__container}>
				{imgLink && (
					<>
						<img className={styles.image} src={imgLink} />
						<div className={styles.bullet}>{queue}</div>
					</>
				)}
			</div>
			<div className={styles.info}>
				{time && <div className={styles.time}>{time}</div>}
				{name && <div className={styles.title}>{name}</div>}
				{address && <div className={styles.address}>{address}</div>}
			</div>
		</button>
	);
};

export default Event;
