import React, { useMemo, type FC } from 'react';
import { type EventCardType } from '../../models/frontend';

import GigachatIcon from '@media/gigachat_icon.svg?react';

import styles from './Card.module.scss';

type CardProps = {
	size?: 'L' | 'M' | 'S';
} & EventCardType;

const Card: FC<CardProps> = ({ size, imgLink, reviews, name, address, description }) => {
	const getCardSize = useMemo(() => {
		switch (size) {
			case 'L':
				return '496px';
			case 'M':
				return '392px';
			case 'S':
				return '239px';
			default:
				return '496px';
		}
	}, [size]);

	return (
		<div className={styles.root} style={{ width: getCardSize }}>
			<img src={imgLink} alt="" className={styles.photo} />
			<div className={styles.info}>
				<div className={styles.title}>{name}</div>
				<div className={styles.address}>{address}</div>
				<div className={styles.description}>{description}</div>
				{reviews && (
					<>
						<div className={styles.reviews__title}>Что выделяют люди</div>
						<div className={styles.reviews__container}>
							{reviews.map((review, i) => (
								<div key={i} className={styles.review}>
									{review}
								</div>
							))}
						</div>
					</>
				)}
				<div className={styles.message}>
					<GigachatIcon className={styles.message__icon} />
					<div className={styles.message__text}>
						Данные собраны из открытых источников и проанализированы нейросетью GigaChat
					</div>
				</div>
				<button className={styles.button}>Посмотреть</button>
			</div>
		</div>
	);
};

export default Card;
