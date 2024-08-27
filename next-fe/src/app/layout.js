import Classes from './Layout.module.scss';

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <head>
                <title>IR Stats</title>
                <link href="https://fonts.googleapis.com/css2?family=Roboto+Condensed&display=swap" rel="stylesheet"></link>
                <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@200..700&display=swap" rel="stylesheet"></link>
                <link href="https://fonts.googleapis.com/css2?family=Teko:wght@300..700&display=swap" rel="stylesheet"></link>
            </head>
            <body className={Classes.layout}>{children}</body>
        </html>
    )
}