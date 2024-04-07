import React, { useState, type FC, useMemo, useEffect, useCallback } from 'react';

import SearchIcon from '@media/search_icon.svg?react';
import { useDebouncedCallback } from 'use-debounce';

import styles from './Input.module.scss';
import Chat from '../Chat';
import { type EventCardType } from '@models/frontend';
import axios, { type AxiosResponse } from 'axios';

export interface ChatMessageType {
	text: string;
	type?: 'ai';
	event?: EventCardType;
	description?: string;
}

interface GigachatMessagesType {
	content: string;
}

const Input: FC = () => {
	const [inputValue, setInputValue] = useState<string>('');
	const [showSuggest, setShowSuggest] = useState<boolean>(false);
	const [showChat, setShowChat] = useState<boolean>(false);
	const [messages, setMessages] = useState<ChatMessageType[]>([]);

	const handleSendMessage = (message: string): void => {
		setMessages((prev) => [{ text: message }, ...prev]);
		axios
			.post<GigachatMessagesType, AxiosResponse<ChatMessageType>>(
				'/api/gigachat/search',
				{
					content: message,
				},
			)
			.then((response) => {
				setMessages((prev) => [response.data, ...prev]);
			})
			.catch((e) => {
				console.log(e);
			});
	};

	const handleNewChat = (): void => {
		axios
			.delete('/api/gigachat/messages/history')
			.then(() => {
				setMessages([]);
			})
			.catch((e) => {
				console.log(e);
			});
	};

	const handleSuggestClick = useCallback((): void => {
		handleSendMessage(inputValue);
		setShowChat(true);
		setShowSuggest(false);
	}, [inputValue]);

	useEffect(() => {
		if (inputValue.length <= 0) {
			setShowSuggest(false);
		}
	}, [inputValue]);

	const suggestText = useMemo(() => {
		return `Попробуйте уточнить у ассистента “${inputValue.charAt(0).toUpperCase() + inputValue.slice(1)}”`;
	}, [inputValue]);

	const debounced = useDebouncedCallback((event: string) => {
		if (!showChat) {
			setShowSuggest(true);
		}
		if (event.length <= 0) {
			setShowSuggest(false);
		}
	}, 1000);

	const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
		setInputValue(event.target.value);
		debounced(event.target.value);
	};

	return (
		<>
			<div className={styles.root}>
				<div className={styles.input__container}>
					<input
						className={styles.input}
						value={inputValue}
						onChange={handleInputChange}
						placeholder="Поиск"
						type="text"
					/>
					<SearchIcon className={styles.icon} />
					{showSuggest && (
						<div className={styles.suggest}>
							<div className={styles.suggest__text}>{suggestText}</div>
							<button className={styles.suggest__button} onClick={handleSuggestClick}>
								Чат
							</button>
						</div>
					)}
				</div>
				<button className={styles.button}>Найти</button>
			</div>
			{showChat && (
				<Chat
					messages={messages}
					sendMessage={handleSendMessage}
					newChat={handleNewChat}
				/>
			)}
		</>
	);
};

export default Input;
