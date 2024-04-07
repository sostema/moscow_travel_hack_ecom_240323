import React, { FC } from "react";

import styles from "./Title.module.scss";

type TitleProps = {
	text: string;
};

const Title: FC<TitleProps> = ({ text }) => {
	return <div className={styles.root}>{text}</div>;
};

export default Title;
