import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setBrowserExecutable(process.env.REMOTION_BROWSER || null);
