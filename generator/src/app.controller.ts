import { Body, Controller, Get, HttpCode, HttpException, Headers, HttpStatus, Post } from '@nestjs/common';
import { AppService } from './app.service';

@Controller('server')
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @Post()
  @HttpCode(200)
  postStatus(@Body() body: {idSender: string, idReceiver: string, msg: string}) {
    console.log("New message sent by '"+ body.idSender+ "' for '"+ body.idReceiver+ "'")
    console.log("Message : ", body.msg);
  }
}
