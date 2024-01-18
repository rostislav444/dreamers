import {Head, Html, Main, NextScript} from 'next/document'
import React from "react";

export default function Document() {
    return (
        <Html lang="uk">
            <Head>
                <link rel="preconnect" href="https://fonts.googleapis.com"/>
                <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin=""/>
                <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600&display=swap"
                      rel="stylesheet"/>
            </Head>
            <body>
            <Main/>
            <NextScript/>
            </body>
        </Html>
    )
}
