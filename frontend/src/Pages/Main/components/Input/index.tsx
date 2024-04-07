import React, { useState, type FC, useMemo, useEffect, useCallback } from 'react';

import SearchIcon from '@media/search_icon.svg?react';
import { useDebouncedCallback } from 'use-debounce';

import styles from './Input.module.scss';
import Chat from '../Chat';
import { type EventCardType } from '@models/frontend';
import axios, { type AxiosPromise, type AxiosResponse } from 'axios';

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
	const [activeLink, setActiveLink] = useState<string>('/api/gigachat/search');

	const handleSendMessage = useCallback(
		(message: string = '', link: string = activeLink): void => {
			if (message) {
				setMessages((prev) => [{ text: message }, ...prev]);
			}
			axios
				.post<GigachatMessagesType, AxiosResponse<ChatMessageType>>(link, {
					content: message,
				})
				.then((response) => {
					setMessages((prev) => [response.data, ...prev]);
				})
				.catch((e) => {
					console.log(e);
				});
		},
		[activeLink],
	);

	const handleNewChat = async (callback?: () => void): AxiosPromise => {
		return await axios.delete('/api/gigachat/messages/history');
	};

	const handleNewChatClick = (): void => {
		handleNewChat()
			.then(() => {
				setActiveLink('/api/gigachat/search');
				setMessages([]);
			})
			.catch((e) => {
				console.log(e);
			});
	};

	const handleSuggestClick = useCallback((): void => {
		handleNewChat()
			.then(() => {
				setMessages([]);
			})
			.then(() => {
				setActiveLink('/api/gigachat/search');
			})
			.then(() => {
				handleSendMessage(inputValue);
				setShowChat(true);
				setShowSuggest(false);
			})
			.catch((e) => {
				console.log(e);
			});
	}, [inputValue]);

	const handleAkinatorClick = (): void => {
		axios
			.delete('/api/gigachat/messages/history')
			.then(() => {
				setMessages([]);
				setActiveLink('/api/gigachat/akinator');
				handleSendMessage('', '/api/gigachat/akinator');
			})
			.catch((e) => {
				console.log(e);
			});
	};

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
					newChat={handleNewChatClick}
					akinatorClick={handleAkinatorClick}
				/>
			)}
		</>
	);
};

export default Input;
