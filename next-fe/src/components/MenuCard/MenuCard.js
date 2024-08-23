import Link from "next/link";
import Classes from "./MenuCard.module.scss";

export default function MenuCard(props) {
    let { link, caption } = props;

    return (
        <Link href={link}>
            <button className={Classes.cardLink}>
                <span>{caption}</span>
            </button>
        </Link>
    )
}