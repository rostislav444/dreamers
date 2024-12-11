import {Grid, GridItem} from "@chakra-ui/react";
import {CameraImage, CameraImagesWrapper} from "@/components/App/Product/Galery/style";
import {MEDIA_URL} from "@/local";

interface ThumbnailsGalleryProps {
    mobile: boolean;
    cameras: any[];
    currentImage: number;
    setCurrentImage: (index: number) => void;
}

const Thumbnails = ({
                               mobile,
                               cameras,
                               currentImage,
                               setCurrentImage
                           }: ThumbnailsGalleryProps) => {
    const handleContextMenuOpen = (e: any) => {
        if (e.target.tagName.toLowerCase() === 'img') {
            e.preventDefault();
        }
    };

    return (
        <Grid
            mt={2}
            mb={4}
            mr={mobile ? 0 : 20}
            w={mobile ? '100%' : '80%'}
            gridTemplateColumns={mobile ? 'repeat(auto-fill, minmax(60px, 1fr))' : 'repeat(auto-fill, minmax(80px, 1fr))'}
            gap={2}
        >
            {cameras.map((camera, key) => (
                <GridItem
                    key={key}
                    onClick={() => setCurrentImage(key)}
                    border={currentImage === key ? '2px solid brown' : '2px solid #fff'}
                    _hover={{
                        borderColor: 'beige',
                    }}
                    cursor='pointer'
                >
                    <CameraImagesWrapper onContextMenu={handleContextMenuOpen} key={key}>
                        {camera.map((image: any, imageKey: number) => (
                            <CameraImage
                                className={'camera-image'}
                                key={imageKey}
                                src={MEDIA_URL + image.thumbnails?.s}
                            />
                        ))}
                    </CameraImagesWrapper>
                </GridItem>
            ))}
        </Grid>
    );
};

export default Thumbnails;