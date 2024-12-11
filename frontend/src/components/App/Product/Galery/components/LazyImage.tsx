import {useEffect, useState} from "react";
import Image from "next/image";
import {LoadFromRoute} from "@/utils/Images/LoadFromRoute";

export const LazyImage = ({lowResSrc, highResSrc, alt}: { lowResSrc: string, highResSrc: string, alt: string }) => {
    const [src, setSrc] = useState<string>(lowResSrc);
    const [isLoaded, setIsLoaded] = useState<boolean>(false);

    useEffect(() => {
        setSrc(lowResSrc);
        setIsLoaded(false);
    }, [lowResSrc, highResSrc]);

    const handleImageLoad = () => {
        setIsLoaded(true);
        setSrc(LoadFromRoute(highResSrc));
    };

    return (
        <Image
            unoptimized={true}
            src={src}
            alt={alt}
            fill={true}
            loading='lazy'
            onLoadingComplete={handleImageLoad}
            style={{
                transition: 'all 0.5s',
                opacity: isLoaded ? 1 : 0.2,
                filter: isLoaded ? 'blur(0)' : 'blur(10px)',
                imageRendering: 'auto',
            }}
        />
    );
};
