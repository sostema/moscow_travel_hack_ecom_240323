import React, { type FC } from 'react';

import styles from './Button.module.scss';

interface ButtonProps {
	text?: string;
	onClick?: () => void;
}

const Button: FC<ButtonProps> = ({ text = 'Спланировать', onClick }) => {
	return (
		<button onClick={onClick} className={styles.root}>
			{text}
		</button>
	);
};

export default Button;
