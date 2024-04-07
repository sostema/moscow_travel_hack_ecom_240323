import React, { useState, type FC, useCallback } from 'react';

import cn from 'classnames';

import GigachatIcon from '@media/gigachat_icon.svg?react';

import styles from './Chat.module.scss';
import Card from '../CardsList/Card';
import { type ChatMessageType } from '../Input';

interface ChatProps {
	messages: ChatMessageType[];
	sendMessage: (message: string) => void;
	newChat: () => void;
}

const Chat: FC<ChatProps> = ({ messages, sendMessage, newChat }) => {
	const [value, setValue] = useState<string>('');

	const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
		setValue(event.target.value);
	};

	const handleInputClick = useCallback((): void => {
		sendMessage(value);
		setValue('');
	}, [value]);

	return (
		<div className={styles.root}>
			<div className={styles.messages__container}>
				{messages.map((message, i) => {
					const isAi = message.type === 'ai';

					return (
						<div
							key={i}
							className={cn(styles.message__wrapper, {
								[styles.message__wrapper__ai]: isAi,
							})}
						>
							<div className={cn(styles.message, { [styles.message__ai]: isAi })}>
								{isAi && <GigachatIcon className={styles.ai__icon} />}
								{message.text}
								{message.description && (
									<div className={styles.ai__description}>{message.description}</div>
								)}
								{message.event && (
									<div className={styles.card__container}>
										<Card {...message.event} size="s" />
									</div>
								)}
							</div>
						</div>
					);
				})}
			</div>
			<div className={styles.bottom__container}>
				<div className={styles.input__container}>
					<input
						className={styles.input}
						value={value}
						onChange={handleInputChange}
						placeholder="Поиск"
					/>
					<button className={styles.sendButton} onClick={handleInputClick}>
						Поиск
					</button>
				</div>
				<div className={styles.customMessages__container}>
					<button className={styles.customMessage} onClick={newChat}>
						Новый чат
					</button>
					<button className={styles.customMessage}>Куда мне сходить еще?</button>
				</div>
			</div>
		</div>
	);
};

export default Chat;
